import React from 'react';
import {FaMinus} from 'react-icons/fa'

interface MinusButtonProps {
    onClick: React.MouseEventHandler,
    size?: number
}

const MinusButton: React.FC<MinusButtonProps> = ({
    onClick,
    size
}) => {
    return (
        <button className="p-3 rounded-lg w-full h-[45px] w-[45px]
                           h-full ring-[1px] ring-gray-300 bg-white hover:shadow-neon
                           flex items-center justify-center"
                type="button"
                onClick={onClick}
        >
            <FaMinus className="fill-black"/>
        </button>
    );
};

export default MinusButton;