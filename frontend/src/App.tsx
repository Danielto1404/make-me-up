import React from 'react';
import LandingPage from "./pages/LandingPage";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import GenerateMakePage from "./pages/GenerateMakePage";
import NotFound404 from "./pages/NotFound404";
import ProfilePage from "./pages/ProfilePage";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route index element={<LandingPage/>}/>
                <Route path="generate" element={<GenerateMakePage/>}/>
                <Route path="me" element={<ProfilePage/>}/>
                <Route path="*" element={<NotFound404/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
