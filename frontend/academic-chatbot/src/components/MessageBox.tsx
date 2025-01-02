"use client";

import React from "react";
import { Box, CircularProgress, Typography } from "@mui/material";

interface MessageBoxProps {
  loading: boolean;
  answer?: string;
}

const MessageBox = ({ answer, loading }: MessageBoxProps) => {
  return (
    <Box
      padding={2}
      border="1px solid #ccc"
      borderRadius="8px"
      bgcolor="#f9f9f9"
    >
      <Typography variant="h6" color="textSecondary">
        {loading && <CircularProgress />}
        {loading ? "Loading..." : answer || "Your answer will appear here"}
      </Typography>
    </Box>
  );
};

export default MessageBox;
