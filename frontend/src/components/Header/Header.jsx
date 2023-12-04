import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Link from '@mui/material/Link';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';

import Drawer from '../Sidebar/Drawer';

const Header = () => {
  return (
    <Box sx={{ display: 'flex' }}>
      <Drawer />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar
          position='static'
          sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
        >
          <Toolbar>
            <IconButton
              size='large'
              edge='start'
              color='inherit'
              aria-label='menu'
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant='h6' component='div' sx={{ flexGrow: 1 }}>
              <Link href='/' color='inherit' underline='none'>
                Github Alerts
              </Link>
            </Typography>
            <Link href='/settings' color='inherit'>
              <Button color='inherit'>Settings</Button>
            </Link>
            <Button color='inherit'>Login</Button>
          </Toolbar>
        </AppBar>
      </Box>
    </Box>
  );
};

export default Header;
