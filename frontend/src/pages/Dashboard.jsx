import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
  IconButton,
} from '@mui/material';
import { Send as SendIcon, Logout as LogoutIcon } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import axios from '../utils/axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [bookmarks, setBookmarks] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async () => {
    try {
      const response = await axios.get('/pages');
      setBookmarks(response.data);
    } catch (error) {
      console.error('Error fetching bookmarks:', error);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('/search', { query: searchQuery });
      setChatHistory([
        ...chatHistory,
        { type: 'user', content: searchQuery },
        { type: 'assistant', content: response.data.results },
      ]);
      setSearchQuery('');
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <Box sx={{ flexGrow: 1, height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ bgcolor: 'primary.main', color: 'white', p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6">bookmark.ai</Typography>
        <IconButton color="inherit" onClick={handleLogout}>
          <LogoutIcon />
        </IconButton>
      </Box>

      <Container maxWidth="xl" sx={{ flexGrow: 1, py: 4 }}>
        <Grid container spacing={3} sx={{ height: '100%' }}>
          {/* Bookmarks List */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ height: '100%', overflow: 'auto' }}>
              <Box sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Your Bookmarks
                </Typography>
                <List>
                  {bookmarks.map((bookmark, index) => (
                    <div key={bookmark.id}>
                      <ListItem>
                        <ListItemText
                          primary={bookmark.title}
                          secondary={bookmark.url}
                        />
                      </ListItem>
                      {index < bookmarks.length - 1 && <Divider />}
                    </div>
                  ))}
                </List>
              </Box>
            </Paper>
          </Grid>

          {/* Chat Interface */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <Box sx={{ p: 2, flexGrow: 1, overflow: 'auto' }}>
                {chatHistory.map((message, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: 'flex',
                      justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                      mb: 2,
                    }}
                  >
                    <Paper
                      sx={{
                        p: 2,
                        maxWidth: '70%',
                        bgcolor: message.type === 'user' ? 'primary.light' : 'grey.100',
                        color: message.type === 'user' ? 'white' : 'text.primary',
                      }}
                    >
                      <Typography>{message.content}</Typography>
                    </Paper>
                  </Box>
                ))}
              </Box>

              <Box
                component="form"
                onSubmit={handleSearch}
                sx={{
                  p: 2,
                  borderTop: 1,
                  borderColor: 'divider',
                  display: 'flex',
                  gap: 1,
                }}
              >
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Ask about your bookmarks..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  disabled={loading}
                />
                <Button
                  type="submit"
                  variant="contained"
                  endIcon={<SendIcon />}
                  disabled={loading || !searchQuery.trim()}
                >
                  Send
                </Button>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Dashboard; 