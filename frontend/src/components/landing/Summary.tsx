import React from 'react';
import {Link} from "react-router-dom";

const Summary = () => {
    return (
        <summary className="bg-black min-h-screen pt-16 flex flex-col items-center">
            <section className="py-10 px-14 ring-1 ring-white font-bold text-white w-fit
                                bg-gradient-to-b from-green-200 to-sky-300
                                bg-clip-text text-transparent">
                <div className="text-8xl">Make.</div>
                <div className="text-7xl">Me.</div>
                <div className="text-6xl">Up.</div>
            </section>
            <section>
                <div className="text-gray-200 text-md mt-16 mb-10 font-semibold">
                    Generate your own makeup which fits you. <br/>
                    Just
                    <span className="decoration-green-200 underline mx-1">prompt</span>
                    a text criteria and
                    <span className="decoration-sky-300 underline mx-1">upload</span>
                    your photo.
                </div>
                <Link to="generate"
                      className="shadow-neon text-black rounded-xl cursor-pointer bg-sky-200
                                 hover:bg-green-100
                                 px-8 py-2 font-semibold text-lg"
                >
                    Try it now!
                </Link>
            </section>
        </summary>
    );
};

export default Summary;