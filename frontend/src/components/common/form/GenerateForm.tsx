import React, {useCallback, useState} from 'react'
import {FormProvider, useForm} from 'react-hook-form'
import {GenerateFormProps} from '../../../types'
import PromptsInput from './PromptsInput'
import UploadUserImage from './UploadUserImage'
import axios, {AxiosRequestConfig} from 'axios'
import Modal from '../Modal'
import Loader from '../Loader'
import {saveAs} from 'file-saver'

const frontViewPhoto = require("../../../resources/front-view-photo.jpg")

const GenerateForm: React.FC = () => {
    const [isUploading, setIsUploading] = useState(false)
    const [generatedSrc, setGeneratedSrc] = useState('')
    const [error, setError] = useState('')
    const [visible, setIsVisible] = useState(false)

    const methods = useForm<GenerateFormProps>({
        defaultValues: {
            media: {
                url: '',
            },
            prompts: [],
        },
    })

    const upload = useCallback(
        (file: File, prompts: string) => {
            const data = new FormData()
            data.append('file', file)
            data.append('prompts', prompts)

            const request: AxiosRequestConfig = {
                url: 'http://localhost:8000/api/v1/transfer',
                method: 'POST',
                data
            }

            setIsUploading(true)
            setError("")
            setGeneratedSrc("")
            setIsVisible(true)
            return axios(request)
        },
        [setIsUploading]
    )

    const onSubmit = useCallback(
        methods.handleSubmit(({prompts, media}) => {
            const file = media.file

            if (!file) {
                methods.setError('media.file', {message: 'Photo is required'})
                return
            }
            if (prompts.length === 0) {
                methods.setError('prompts.0.prompt', {
                    message: 'At least one criteria must be filled',
                })
            }

            upload(file, prompts.map((p) => p.prompt).join('|'))
                .then(response => {
                    const data = response.data
                    if (data.status_code !== 200) {
                        setError(data.detail)
                    } else {
                        setGeneratedSrc(`data:image/jpeg;base64,${data.base64_image}`)
                    }
                })
                .catch(e => setError(e.message))
                .finally(() => setIsUploading(false))
        }),
        [methods]
    )

    const [url, prompts] = methods.watch(['media.url', 'prompts'])

    return (
        <>
            <FormProvider {...methods}>
                <form
                    onSubmit={onSubmit}
                    encType="multipart/form-data"
                >
                    <div className="flex flex-row items-end gap-20 justify-between pb-12">
                        <div className="space-y-14">
                            <PromptsInput/>
                            <UploadUserImage/>
                        </div>
                        <div className="max-w-[35%] rounded-2xl bg-white p-2">
                            <div className="font-archivo text-lg text-black text-center font-bold">
                                Make a front view photo
                            </div>
                            <img src={frontViewPhoto}
                                 alt="front-view"
                                 className="object-contain"
                            />
                        </div>
                    </div>
                    <button
                        onClick={onSubmit}
                        disabled={
                            !methods.formState.isValid ||
                            !url ||
                            prompts.length === 0 ||
                            prompts.filter((p) => !p.prompt).length !== 0
                        }
                        className="disabled:opacity-50
                                   mb-12
                                   bg-gradient-to-br
                                   from-green-100 to-sky-200
                                   disabled:hover:from-green-100
                                   disabled:hover:to-sky-200
                                   hover:from-sky-200
                                   hover:to-pink-300
                                   rounded-xl px-6 py-3 text-black font-semibold"
                    >
                        Generate
                    </button>
                </form>
            </FormProvider>
            {visible &&
                <Modal close={() => setIsVisible(false)}>
                    <div
                        className="font-archivo text-black
                                   text-center ring-2 ring-white rounded-2xl bg-white
                                   p-5 min-w-[400px] shadow-neon"
                    >
                        {isUploading && (
                            <>
                                <div className="text-2xl">
                                    Generating makeup...
                                </div>
                                <div className="text-sm text-gray-500 mb-5">
                                    It usually takes up to 20 seconds
                                </div>
                                <Loader/>
                            </>
                        )}
                        {error &&
                            <div className="w-full px-4 text-lg flex flex-col text-xl items-center gap-6">
                                {error}
                                <button className="text-white bg-purple-400 hover:bg-purple-500 rounded-xl px-4 py-2"
                                        onClick={() => setIsVisible(false)}>
                                    Try again
                                </button>
                            </div>
                        }
                        {generatedSrc && (
                            <div className="flex flex-col justify-center items-center">
                                <img src={generatedSrc}
                                     alt={prompts.map(p => p.prompt).join(',')}
                                />
                                <button
                                    className="mt-5 text-black rounded-xl cursor-pointer bg-sky-200
                                               hover:bg-sky-300
                                               px-8 py-2 font-semibold text-md"
                                    onClick={() => {
                                        saveAs(
                                            generatedSrc,
                                            'generated.png'
                                        )
                                        methods.resetField('media')
                                        methods.resetField('prompts')
                                    }}
                                >
                                    Save photo
                                </button>
                            </div>
                        )}
                    </div>
                </Modal>
            }
        </>
    )
}

export default GenerateForm
