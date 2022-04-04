import React from 'react';

const GradientText: React.FC<{ text: string, classes?: string }> = ({
    text,
    classes
}) => {
    return (
        <div className={`bg-clip-text text-transparent ${classes}`}>
            {text}
        </div>
    );
};

export default GradientText;