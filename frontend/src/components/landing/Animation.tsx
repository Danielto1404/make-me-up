import React from 'react';

const workflow = require("../../resources/workflow.png")

const Animation = () => {
    return (
        <div className="bg-gradient-to-br from-green-200 to-sky-300 min-h-screen pt-16 flex flex-col items-center">
            <img src="https://media.giphy.com/media/pZwQz0w8bYcZW/giphy.gif" alt="loading.."/>
            <img src={workflow} alt="loading.." width={500} className="mt-10"/>
        </div>
    );
};

export default Animation;