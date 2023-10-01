import Container from '@mui/material/Container';
import './Home.css';
import Typography from '@mui/material/Typography';

const Home = (props) => {
  return (
    <>
      <Container maxWidth='sm'>
        <Typography variant='h4'>
          <div className='title-home'>Welcome to GH Alerts!</div>
        </Typography>
      </Container>
    </>
  );
};

export default Home;
