import { Box, Button, Container, Typography, Grid, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LandingPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 8,
          textAlign: 'center',
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h2" component="h1" gutterBottom>
            bookmark.ai
          </Typography>
          <Typography variant="h5" component="h2" gutterBottom>
            Your AI-Powered Bookmark Manager
          </Typography>
          <Typography variant="body1" paragraph>
            Organize, search, and discover your bookmarks with the power of artificial intelligence.
          </Typography>
          <Button
            variant="contained"
            color="secondary"
            size="large"
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/login')}
            sx={{ mt: 2 }}
          >
            {isAuthenticated ? 'Go to Dashboard' : 'Get Started'}
          </Button>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Typography variant="h5" component="h3" gutterBottom>
                Smart Organization
              </Typography>
              <Typography>
                Automatically categorize and tag your bookmarks using AI technology.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Typography variant="h5" component="h3" gutterBottom>
                Natural Language Search
              </Typography>
              <Typography>
                Find your bookmarks using natural language queries and conversational AI.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Typography variant="h5" component="h3" gutterBottom>
                Cross-Platform Sync
              </Typography>
              <Typography>
                Access your bookmarks from any device, anywhere, anytime.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box sx={{ bgcolor: 'grey.100', py: 8 }}>
        <Container maxWidth="md" sx={{ textAlign: 'center' }}>
          <Typography variant="h4" component="h2" gutterBottom>
            Ready to transform your bookmarking experience?
          </Typography>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/register')}
            sx={{ mt: 2 }}
          >
            {isAuthenticated ? 'Go to Dashboard' : 'Sign Up Now'}
          </Button>
        </Container>
      </Box>
    </Box>
  );
};

export default LandingPage; 