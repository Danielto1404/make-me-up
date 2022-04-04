import React from 'react';

interface PreviewUploadedImageProps {
    imageUrl: string
    clear: () => void
}

const PreviewUploadedImage: React.FC<PreviewUploadedImageProps> = ({
    imageUrl,
    clear
}) => {
    return (
        <div className="p-2 relative border-2 border-gray-300 border-dashed w-full h-full inherit-border">
            <div className="h-full w-full relative overflow-hidden flex items-center justify-center inherit-border">
                <img src={imageUrl} alt="loading.." className="w-full h-full object-cover inherit-border"/>
            </div>
            <button type="button"
                    className="-top-3 -right-3 bg-gray-900 text-white absolute z-[50]
                               rounded-full hover:bg-gray-500 cursor-pointer"
                    onClick={clear}
            >
                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="white"
                     viewBox="0 0 24 24"
                     stroke="white" aria-hidden="true">
                    <path d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        </div>
    );
};

export default PreviewUploadedImage;