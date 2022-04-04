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
        <button className="p-3 rounded-lg w-full aspect-w-1 aspect-h-1
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