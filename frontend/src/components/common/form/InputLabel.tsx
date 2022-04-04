import React, {memo} from 'react';

interface RequiredFiledLabelProps {
    label: string
    description?: string | React.ReactNode,
    required?: boolean
}

const InputLabel: React.FC<RequiredFiledLabelProps> = ({
    label,
    description,
    required
}) => {

    return (
        <span className="flex flex-col text-xl text-white font-semibold mb-2">
            <span className={`inline-flex gap-1 items-center`}>
                {required && <b className="text-red-300 font-black">*</b>}
                {label}
            </span>
            {description &&
                <span className="text-gray-300 text-[13px] font-semibold">
                    {description}
                </span>
            }
        </span>
    );
};

export default memo(InputLabel);