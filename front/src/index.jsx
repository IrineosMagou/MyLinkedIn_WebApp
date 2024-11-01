import React from 'react'
import WelcomePage from './Welcome/WelcomePage';
import { BrowserRouter as Router, Route, Routes  , Outlet} from 'react-router-dom';
import SignIn from './Welcome/SignIn';
import SignUp from './Welcome/SignUp';
import SettingsOptions from './account_settings/settings_options';
import ChangePassword from './account_settings/change_password';
import ProfilePicture from './Welcome/insert_pictures';
import Network from './Network/network';
import ChangeUsername from './account_settings/change_username';
import UserBlog from './Network/user_blog';
import Notifications from './account_settings/Notifications';
import FullArticle from './articles/full_article';
import UploadArticle from './articles/upload_article';
import Layout from './layout';
import ChatComponent from './chat/communication';
import CheckChat from './chat/check';
import PersonalInfoForm from './account_settings/personal_info';
import ConnectedAds from './ads/ad_grid';
import FullAd from './ads/full_ad';
import UploadAd from './ads/upload_ad';
import AllUsers from './admin/admin_first';
import UserView from './admin/user_view';
import ManageArticle from './articles/manage_article';
import ManageAd from './ads/manage_ad';
const WithNavbar = () => (
  <Layout>
    <Outlet /> {/* Outlet renders the nested route content here */}
  </Layout>
);


const RouterSetup = () => {
  return (
    <Router>
      <Routes>
        <Route element={<WithNavbar/>}>
          <Route exact path='/' element={<WelcomePage />}/> 
          <Route exact path='/SignIn' element={<SignIn/>}/>       
          <Route exact path='/SignUp' element={<SignUp />}/>
          <Route exact path='/account_settings' element={<SettingsOptions/>}/>
          <Route exact path='/change_password' element={<ChangePassword/>}/>
          <Route exact path='/network' element={<Network/>}/>
          <Route exact path='/change_username' element={<ChangeUsername/>}/>
          <Route exact path='user_profile/picture' element={<ProfilePicture/>}/>
          <Route path="/user_blog/:user_id" element={<UserBlog />} />
          <Route path="/chat/:room_id" element={<ChatComponent />} />
          <Route path="/chat" element={<ChatComponent />} />
          <Route path="/user_notifications" element={<Notifications />} />
          <Route path="/read_article/:article_id" element={<FullArticle />} />
          <Route path="/upload_article" element={<UploadArticle />} />
          <Route path="/check_chat" element={<CheckChat />} />
          <Route path="/personal_info" element={<PersonalInfoForm />} />
          <Route path="/ads" element={<ConnectedAds />} />
          <Route path="/read_ad/:ad_id" element={<FullAd />} />
          <Route path="/upload_ad" element={<UploadAd/>} />
          <Route path="/article_manage/:article_id" element={<ManageArticle/>} />
          <Route path="/ad_manage/:ad_id" element={<ManageAd/>} />
        </Route>

        <Route path="/admin_users" element={<AllUsers/>} />
        <Route path="/admin_user_view/:user_id" element={<UserView/>} />
      </Routes>
    </Router>

  )
}

export default RouterSetup