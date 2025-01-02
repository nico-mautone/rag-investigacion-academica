"use client";

import React from "react";
import ChatQueryBar from "./ChatQueryBar";
import MessageBox from "./MessageBox";
import axios from "axios";

const ChatBot = () => {
  const [query, setQuery] = React.useState("");
  const [answer, setAnswer] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  const handleSendQuery = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/query", {
        query,
      });
      console.log("Response:", response.data);
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Error:", error);
    }
    setLoading(false);
  };

  const handleChangeQuery = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  return (
    <>
      <ChatQueryBar
        onClickSend={handleSendQuery}
        query={query}
        handleChangeQuery={handleChangeQuery}
      />
      <MessageBox answer={answer} loading={loading} />
    </>
  );
};

export default ChatBot;
