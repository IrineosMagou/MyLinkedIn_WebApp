import ConnectedArticles from '../articles/article_grid';
import { Container } from '@mui/material';

const WelcomePage = () => {

  return (
    <Container maxWidth="lg" style={{ marginTop: '20px' }}>
        <div style={styles.container}>
          <h3>
              Συνδέσου με Επαγγελματίες από ολο τον κόσμο !
          </h3>
        <div style={styles.container}>
        <ConnectedArticles />
        </div>
      </div>
    </Container>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '0 20px',
    textAlign: 'center',
  },
  heading: {
    fontSize: '2rem',
    color: '#333',
    margin: '20px 0',
  },
  paragraph: {
    fontSize: '1.2rem',
    color: '#666',
    maxWidth: '600px',
  },
};

export default WelcomePage;
