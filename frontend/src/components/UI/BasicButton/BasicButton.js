import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';

const BasicButton = (props) => {
  return (
    <Stack spacing={2} direction='row'>
      <Button variant='contained'>{props.label}</Button>
    </Stack>
  );
};

export default BasicButton;
