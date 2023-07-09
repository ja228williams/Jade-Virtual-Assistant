import React from 'react';

import PreviousMessage from './PreviousMessage';

export default function ChatHistory({ messages }) {
    // messages should be an array of [text, "user"/"jade"] pairs
    // console.log("messages:", messages);
    return (
        <div id="chat-history">
            {messages?.map((message, index) => {
                // console.log("mapping message: " + message);
                return <PreviousMessage message={message} key={index}/>;
            })}
        </div>
    );
}