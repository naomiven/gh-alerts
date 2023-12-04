import Divider from '@mui/material/Divider';
import MuiDrawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import Toolbar from '@mui/material/Toolbar';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';

import { drawerItems } from './DrawerItems';

const drawerWidth = 240;

const Drawer = () => {
  return (
    <MuiDrawer variant='permanent' /*open={open}*/>
      <Toolbar
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-end',
          px: [1],
        }}
      >
        <IconButton /*onClick={toggleDrawer}*/>
          <ChevronLeftIcon />
        </IconButton>
      </Toolbar>
      <Divider />
      <List component='nav'>
        {drawerItems}
        <Divider sx={{ my: 1 }} />
      </List>
    </MuiDrawer>
  );
};

export default Drawer;
