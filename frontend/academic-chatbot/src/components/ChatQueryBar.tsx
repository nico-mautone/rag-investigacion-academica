"use client";

import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";

interface ChatQueryBarProps {
  onClickSend: () => void;
  query: string;
  handleChangeQuery: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const ChatQueryBar = ({
  onClickSend,
  query,
  handleChangeQuery,
}: ChatQueryBarProps) => {
  return (
    <Box display="flex" alignItems="center" gap={2}>
      <TextField
        label="Search"
        variant="outlined"
        value={query}
        onChange={handleChangeQuery}
        fullWidth
      />
      <Button variant="contained" color="primary" onClick={onClickSend}>
        Send
      </Button>
    </Box>
  );
};

export default ChatQueryBar;
