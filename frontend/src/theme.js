import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#8caaee',
    },
    secondary: {
      main: '#94e2d5',
    },
    background: {
      default: '#1e1e2e',
      drawer: '#45475a',
      paper: '#fff', // White background for components such as Cards and Paper
    },
    text: {
      primary: '#cdd6f4',
      secondary: '#f5c2e7',
    },
    appBar: {
      main: '#1e1e2e',
    },
  },
});

export default theme;
