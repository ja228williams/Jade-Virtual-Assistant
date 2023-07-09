console.log("App pre-import log");

import React from 'react';

import Header from './Header';
import Chat from './Chat';
import SpeechToText from './SpeechToText';

console.log("App post-import log");

export default function App() {
    return (
        <>
            <Header/>
            <SpeechToText/>
            <Chat id="chat"/>
        </>
    )
}