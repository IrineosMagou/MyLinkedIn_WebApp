import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, Card, CardContent, Avatar, Typography } from '@mui/material';

// Profile on the Grid Component
export function ProfileGrid({ user, onClick }) {
  return (
    <Card onClick={onClick} sx={{ cursor: 'pointer', maxWidth: 345 }}>
      <CardContent>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Avatar
              src={'http://127.0.0.1:8000' + user.avatar}
              alt={`${user.name}'s avatar`}
              sx={{ width: 56, height: 56 }}
            />
          </Grid>
          <Grid item>
            <Typography variant="h6">{user.name}</Typography>
            <Typography variant="body2" color="textSecondary">
              {user.email}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {user.phone}
            </Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

// Profile in the User Blog Component
export function UserProfile({ user }) {
  return (
    <Card sx={{ maxWidth: 600, margin: '0 auto' }}>
      <CardContent>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Avatar
              src={'http://127.0.0.1:8000' + user.avatar}
              alt={`${user.name}'s avatar`}
              sx={{ width: 100, height: 100 }}
            />
          </Grid>
          <Grid item xs={12}>
            <Typography variant="h5">{user.name} {user.surname}</Typography>
            <Typography variant="body1">Profession: {user.profession}</Typography>
            <Typography variant="body1">Email: {user.email}</Typography>
            <Typography variant="body1">Phone: {user.phone}</Typography>
            {user.skills && <Typography variant="body1">Skills: {user.skills}</Typography>}
            {user.age && <Typography variant="body1">Age: {user.age}</Typography>}
            {user.education && <Typography variant="body1">Education: {user.education}</Typography>}
            {user.experience && <Typography variant="body1">Experience: {user.experience}</Typography>}
            {user.employment && <Typography variant="body1">Employment: {user.employment}</Typography>}
            {user.connection_status === 'Rejected' && (
              <Typography variant="body2" color="error">
                Αίτημα Σύνδεσης: Απορρίφθηκε
              </Typography>
            )}
            {user.connection_status === 'Pending' && (
              <Typography variant="body2" color="warning.main">
                Αίτημα Σύνδεσης: Εκκρεμεί
              </Typography>
            )}
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

// UserGrid Component
const UserGrid = ({ users }) => {
  const navigate = useNavigate();

  const handleUserClick = (user_id) => {
    navigate(`/user_blog/${user_id}`);
  };

  if (!users || users.length === 0) {
    return <Typography variant="body1">Δεν έχετε κάποια σύνδεση. Βρείτε επαγγελματίες μέσω αναζήτησης!</Typography>;
  }

  return (
    <Grid container spacing={2}>
      {users.map((user, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <ProfileGrid user={user} onClick={() => handleUserClick(user.id)} />
        </Grid>
      ))}
    </Grid>
  );
};

export default UserGrid;
