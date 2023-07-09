import React, { useState } from 'react';

export default function ChatMessage({ onMsgSubmit }) {
    const [msg, setMsg] = useState('');

    const handleUserInput = ({ target }) => {
        setMsg(target.value);
    }

    const handleEnter = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            console.log("submitted: " + msg);
            onMsgSubmit(msg);
            setMsg("");
        }
    }

    return (
        <div>
            <form>
                <textarea type="text" id="input-msg" value={msg} onKeyDown={handleEnter} onChange={handleUserInput}/>
            </form>
        </div>
    );
}