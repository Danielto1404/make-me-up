import React, {memo, useCallback} from 'react';
import {useFormContext} from "react-hook-form";
import UploadImage from "./image/UploadImage";
import {MediaInput} from "../../../types";
import InputLabel from "./InputLabel";

const UploadUserImage: React.FC = () => {

    const {register, formState, resetField, watch, setValue} = useFormContext<{ media: MediaInput }>()

    const reset = useCallback(() => {
        resetField("media")
        resetField("media")
    }, [resetField])

    const url = watch("media.url")

    return (
        <div>
            <InputLabel label="Your photo"
                        required={true}
                        description="Upload your photo for making makeup transfer"
            />
            <UploadImage wrapperClasses="w-[300px] h-[300px] rounded-xl"
                         url={url}
                         reset={reset}
                         error={formState?.errors?.media?.file?.message}
                         imageInputProps={
                             register("media", {
                                 onChange: event => {
                                     const file = event.target.files[0]
                                     setValue("media.file", file)
                                     setValue("media.url", URL.createObjectURL(file))
                                 }
                             })
                         }
            />
        </div>
    );
};

export default memo(UploadUserImage);