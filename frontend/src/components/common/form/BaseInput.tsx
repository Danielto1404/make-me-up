import React from 'react';
import {BiErrorCircle} from 'react-icons/bi'
import {classNames} from "../../../utils";

export type ReactInputProps = React.DetailedHTMLProps<React.InputHTMLAttributes<HTMLInputElement>, HTMLInputElement>
export type BaseInputProps = ReactInputProps & {
    error?: string,
}

const BaseInput = React.forwardRef<HTMLInputElement, BaseInputProps>(
    (props, ref
    ) => {

        const {error, children, ...inputProps} = props

        return (
            <div className="font-archivo flex flex-col justify-start w-full text-white max-w-[300px]

            ">
                <div className="items-center inline-flex gap-3 w-full">
                    <div className={
                        classNames("w-full flex transition-all focus-within:shadow-neon " +
                            " rounded-lg overflow-hidden ring-gray-300 ring-[1px]",
                            error ? "ring-red-400" : "ring-gray-100"
                        )}
                    >
                        <input ref={ref}
                               className="w-full outline-none border-0 bg-transparent px-4 my-3
                                      focus:ring-0 font-archivo font-semibold text-[12px] md:text-[14px]"
                               {...inputProps}
                        />
                    </div>
                    {children}
                </div>
                {error &&
                    <div className="text-red-500 text-[13px] mt-3 ml-1 inline-flex gap-2 items-center">
                        <BiErrorCircle className="fill-red-500" size={18}/>
                        {error}
                    </div>
                }
            </div>
        );
    });

export default BaseInput;