import React, {useCallback, useState} from 'react';
import {FormProvider, useForm} from "react-hook-form";
import {GenerateFormProps} from "../../../types";
import PromptsInput from "./PromptsInput";
import UploadUserImage from "./UploadUserImage";
import axios, {AxiosRequestConfig} from "axios";
import Modal from "../Modal";
import Loader from "../Loader";
import {saveAs} from "file-saver";

const GenerateForm: React.FC = () => {

    const [isUploading, setIsUploading] = useState(false)
    const [generatedSrc, setGeneratedSrc] = useState('')

    const methods = useForm<GenerateFormProps>({
        defaultValues: {
            media: {
                url: ''
            },
            prompts: []
        }
    })

    const upload = useCallback((file: File, prompts: string) => {

        const data = new FormData()
        data.append("file", file)
        data.append("prompts", prompts)

        const request: AxiosRequestConfig = {
            url: "http://localhost:8000/api/v1/transfer",
            method: "POST",
            data,
            responseType: "arraybuffer"
        }

        setIsUploading(true)
        return axios(request)

    }, [setIsUploading])

    const onSubmit = useCallback(methods.handleSubmit(({
        prompts,
        media
    }) => {

        const file = media.file

        if (!file) {
            methods.setError("media.file", {message: "Photo is required"})
            return
        }
        if (prompts.length === 0) {
            methods.setError("prompts.0.prompt", {
                message: "At least one criteria must be filled"
            })
        }

        upload(file, prompts.map(p => p.prompt).join("|"))
            .then(response => new Blob([response.data]))
            .then(blob => setGeneratedSrc(URL.createObjectURL(blob)))
            .catch(e => alert(e))
            .finally(() => setIsUploading(false))

    }), [methods])


    const [url, prompts] = methods.watch(["media.url", "prompts"])

    return (
        <>
            <FormProvider {...methods}>
                <form onSubmit={onSubmit} className="space-y-14 pb-12 px-6" encType="multipart/form-data">
                    <PromptsInput/>
                    <UploadUserImage/>
                    <button onClick={onSubmit}
                            disabled={
                                !methods.formState.isValid
                                || !url
                                || prompts.length === 0
                                || prompts.filter(p => !p.prompt).length !== 0
                            }
                            className="disabled:opacity-50 bg-gradient-to-br from-green-100 to-sky-200
                                   rounded-xl px-6 py-3 text-black font-semibold">
                        Generate
                    </button>
                </form>
            </FormProvider>
            {isUploading || generatedSrc &&
                <Modal>
                    <div className="font-archivo text-white w-full text-center">
                        {isUploading &&
                            <>
                                <div className="text-2xl">Generating makeup...</div>
                                <div className="text-sm opacity-80 mb-5">It usually takes up to 40 seconds</div>
                                <Loader/>
                            </>
                        }
                        {generatedSrc &&
                            <div className="flex flex-col justify-center items-center">
                                <img src={generatedSrc}/>
                                <button
                                    className="mt-5 text-black rounded-xl cursor-pointer bg-sky-200
                                               hover:bg-green-100
                                               hover:shadow-neon
                                               px-8 py-2 font-semibold text-md"
                                    onClick={() => {
                                        saveAs(generatedSrc, "generated.png")
                                        methods.resetField("media")
                                        methods.resetField("prompts")
                                    }}
                                >
                                    Save photo
                                </button>
                            </div>
                        }
                    </div>
                </Modal>
            }
        </>
    );
};

export default GenerateForm;
