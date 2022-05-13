import React from 'react';

interface TogglePropsTypes {
    text: string
    handleToggle: (checked: boolean) => any
    defaultChecked?: boolean
}

const Toggle: React.FC<TogglePropsTypes> = ({
    text,
    handleToggle,
    defaultChecked = false
}) => {
    return (
        <div className="inline-flex items-center">
            <div className="mr-5 text-white font-archivo text-lg">
                {text}
            </div>
            <label htmlFor={`blueToggle-${text}`}>
                <div className="relative cursor-pointer">
                    <input type="checkbox" id={`blueToggle-${text}`} className="sr-only"
                           defaultChecked={defaultChecked}
                           onChange={e => handleToggle(e.target.checked)}/>
                    <div
                        className="checkedBackground ring-1 ring-inset w-[56px] h-[28px] rounded-full
                                   transition duration-100 ease-linear"
                    />
                    <div
                        className="dotCheckbox absolute left-[4px] top-[4px] bg-blue-200 w-[20px] h-[20px]
                                   rounded-full transition duration-100 ease-linear"
                    />
                </div>
            </label>
        </div>
    );
}

export default Toggle;