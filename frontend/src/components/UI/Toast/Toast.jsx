import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant='filled' {...props} />;
});

const Toast = (props) => {
  return (
    <Stack spacing={2} sx={{ width: '100%' }}>
      <Snackbar
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        open={props.open}
        autoHideDuration={3000}
        onClose={props.onClose}
      >
        <Alert
          onClose={props.onClose}
          severity='success'
          sx={{ width: '100%' }}
        >
          {props.message}
        </Alert>
      </Snackbar>
    </Stack>
  );
};

export default Toast;
