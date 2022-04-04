import React from 'react';
import {BiErrorCircle} from "react-icons/bi";
import {NoRefInputProps} from "../../../../types";
import UploadMediaIcon from "../../icons/UploadMediaIcon";

const UploadImageBlock = React.forwardRef<HTMLInputElement, NoRefInputProps & { error?: string }>(
    (props, ref) => {
        const {error, ...inputProps} = props
        return (
            <>
                <div className="p-2 relative border-2 border-gray-300 border-dashed w-full h-full inherit-border">
                    <div className="space-y-1 text-center flex flex-col items-center justify-center h-full w-full">
                        <div className="flex text-sm text-gray-600">
                            <label className="mx-auto cursor-pointer rounded-md font-medium
                                             text-blue-400 hover:text-indigo-400
                                             focus:outline-none
                                             focus-visible:ring-0"
                            >
                                <UploadMediaIcon/>
                                Upload image
                                <input {...inputProps}
                                       ref={ref}
                                       type="file"
                                       accept="image/jpeg, image/png"
                                       className="sr-only"
                                />
                                <p className="text-xs text-gray-300">
                                    PNG, JPG, GIF up to 10MB
                                </p>
                            </label>
                        </div>
                    </div>
                </div>
                {error &&
                    <div
                        className="text-red-500 text-[13px] mt-3 ml-1 inline-flex gap-2 font-medium items-center font-archivo">
                        <BiErrorCircle className="fill-red-500" size={18}/>
                        {error}
                    </div>
                }
            </>
        );
    });

export default UploadImageBlock;