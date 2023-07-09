import React from 'react';

// just have this consist of text for now
export default function PreviousMessage({ message }) {
    console.log('generating message' + message);
    const [text, sender] = message;
    // const text = message[0];
    // const sender = message[1] === "user" ? "me" : "jade";
    return (
        <p className="prev-msg" id={"sender-" + sender}>{sender}: {text}</p>
    );
}