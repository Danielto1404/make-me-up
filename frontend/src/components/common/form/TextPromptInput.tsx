import React from 'react';
import BaseInput from "./BaseInput";
import PlusButton from "../buttons/PlusButton";

const TextPromptInput = () => {
    return (
        <div className="text-white font-semibold">
            <div className="text-xl">
                Text prompt
            </div>
            <div className="text-gray-300 text-[13px] mb-4">
                You can add text promt related to make which you want to fit
            </div>
            <div className="inline-flex gap-2">
                <PlusButton onClick={() => console.log()}/>
                <BaseInput placeholder="red lips"/>
            </div>
        </div>
    );
};

export default TextPromptInput;