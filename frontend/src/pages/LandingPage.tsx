import React from 'react';

import Animation from "../components/landing/Animation";
import Summary from "../components/landing/Summary";

const LandingPage = () => {
    return (
        <div className="grid grid-cols-[2fr_3fr]">
            <Summary/>
            <Animation/>
        </div>
    );
};

export default LandingPage;