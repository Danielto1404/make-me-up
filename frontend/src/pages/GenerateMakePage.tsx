import React from 'react';
import GenerateForm from "../components/common/form/GenerateForm";

const GenerateMakePage = () => {
    return (
        <div className="min-h-screen bg-black">
            <div className="mx-auto max-w-[900px]">
                <div className="text-6xl pt-10 text-center text-white font-bold mb-12 text-transparent
                                bg-gradient-to-br bg-clip-text from-blue-400 to-green-100">
                    Generate your own make
                </div>
                <GenerateForm/>
            </div>
        </div>
    );
};

export default GenerateMakePage;