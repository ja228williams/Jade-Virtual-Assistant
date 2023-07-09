import React, { useState, useEffect } from 'react';

import ChatHistory from './ChatHistory';
import ChatMessage from './ChatMessage';

export default function Chat() {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        window.electronAPI.receiveJadeMsg((_event, msg, user) => {
            console.log("received msg from " + user + ": " + msg);
            receiveNewMsg(msg, user);
        });
    }, []);

    const handleMsgSubmit = msg => {
        receiveNewMsg(msg, 'user');

        // send to main
        window.electronAPI.sendMsgToJade(msg);
    };

    const receiveNewMsg = (msg, sender) => {
        console.log('received msg: ' + msg);
        setHistory(prevHistory => 
            [
                ...prevHistory, 
                [msg, sender]
            ]
        );
    };

    return (
        <div id="chat">
            <ChatHistory messages={history}/>
            <ChatMessage onMsgSubmit={handleMsgSubmit}/>
        </div>
    );
}