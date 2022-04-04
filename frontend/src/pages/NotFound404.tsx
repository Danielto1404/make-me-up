import React from 'react';
import {Link} from "react-router-dom";

const NotFound404Page = () => {
    return (
        <div className="h-screen bg-black">
            <div className="text-white font-bold text-4xl pt-40 text-center flex flex-col items-center">
                404. Page not found.
                <Link to="/" className="mt-10 px-6 py-3 bg-blue-400 w-fit rounded-3xl text-xl">
                    Back to home
                </Link>
            </div>
        </div>
    );
};

export default NotFound404Page