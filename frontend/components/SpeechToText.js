import React, { useState, useEffect } from 'react';

export default function SpeechToText() {
  console.log("speech to text button rendering");

  const [sttEnabled, setSttEnabled] = useState(false);

  const handleClick = () => {
    console.log("stt button clicked!");
    const updatedSttEnabled = !sttEnabled;
    setSttEnabled(updatedSttEnabled);
    console.log("sttEnabled:", updatedSttEnabled);
    // send to main
    window.electronAPI.sttToggle(updatedSttEnabled);
  };

  useEffect(() => {
    window.electronAPI.sttSetState((_event, state) => {
        console.log("setting state to " + state);
        setSttEnabled(state);
    });
}, []);

  const buttonClassName = sttEnabled ? 'enabled' : 'disabled';

  return (
    <button type="button" id="speechtotext" className={buttonClassName} onClick={handleClick}>
      Speech to Text
    </button>
  );
}
