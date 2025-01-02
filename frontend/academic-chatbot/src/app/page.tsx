import { Box, Container, Typography } from "@mui/material";
import ChatBot from "@/components/ChatBot";

export default function Home() {
  return (
    <Container maxWidth="sm" style={{ marginTop: "50px" }}>
      <Typography variant="h4" textAlign="center" gutterBottom>
        Simple Page with Search Bar and Message Box
      </Typography>
      <Box display="flex" flexDirection="column" gap={4}>
        <ChatBot />
      </Box>
    </Container>
  );
}
