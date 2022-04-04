import React from 'react';
import UploadImageBlock from "./UploadImageBlock";
import PreviewUploadedImage from "./PreviewUploadedImage";
import RoundedSizeWrapperContainer from "./RoundedSizeWrapperContainer";
import {NoRefInputProps} from "../../../../types";

interface UploadImageProps {
    imageInputProps: NoRefInputProps
    error?: string,
    url?: string
    reset: () => void,
    wrapperClasses?: string
}

const UploadImage: React.FC<UploadImageProps> = ({
    imageInputProps,
    reset,
    error,
    url,
    wrapperClasses
}) => {

    return (
        <RoundedSizeWrapperContainer classes={wrapperClasses}>
            <div className="text-[15px] font-bold text-gray-700 w-full h-full inherit-border">
                {url
                    ? <PreviewUploadedImage imageUrl={url} clear={reset}/>
                    : <UploadImageBlock error={error} {...imageInputProps}/>
                }
            </div>
        </RoundedSizeWrapperContainer>
    )
};

export default UploadImage;
