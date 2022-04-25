import React, {useCallback} from 'react';
import {FormProvider, useForm} from "react-hook-form";
import {GenerateFormProps} from "../../../types";
import PromptsInput from "./PromptsInput";
import UploadUserImage from "./UploadUserImage";
import axios, {AxiosRequestConfig, AxiosResponse} from "axios";

const GenerateForm: React.FC = () => {

    const methods = useForm<GenerateFormProps>({
        defaultValues: {
            media: {
                url: ''
            },
            prompts: []
        }
    })

    // const onNext = useCallback(async res => {
    //     const data = await res.json();
    //     console.log(data)
    // }, []);
    //
    // useStream('http://localhost:8000/generate', {onNext});

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
            // return;
        }

        console.log(file)


        const formData = new FormData()
        formData.append("img", file.name)

        axios({
            url: "http://localhost:8000/api/v1/transfer",
            method: "POST",
            data: formData,
            headers: {
                "Content-Type": "multipart/form-data"
            }

        }).then(r => console.log(r.data)).catch(e => console.log(e.message))

    }), [methods])


    const url = methods.watch("media.url")

    return (
        <FormProvider {...methods}>
            <form onSubmit={onSubmit} className="space-y-14 pb-12" encType="multipart/form-data">
                <PromptsInput/>
                <UploadUserImage/>
                <button onClick={onSubmit}
                        disabled={!methods.formState.isValid || !url}
                        className="disabled:opacity-50 bg-gradient-to-br from-green-100 to-sky-200
                                   rounded-xl px-6 py-3 text-black font-semibold">
                    Generate
                </button>
            </form>
        </FormProvider>
    );
};

export default GenerateForm;
