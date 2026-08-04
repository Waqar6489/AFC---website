import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { FiCheckCircle, FiXCircle } from 'react-icons/fi';
import AuthCard from '@/components/common/AuthCard';
import PageLoader from '@/components/ui/PageLoader';
import { authService } from '@/services/authService';
import { extractApiError } from '@/services/apiClient';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { tokenStorage } from '@/utils/tokenStorage';

export default function VerifyEmailPage() {

  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setUser } = useAuth();
  const uid = searchParams.get('uid');
  const token = searchParams.get('token');
  const [status, setStatus] = useState('verifying'); // verifying | success | error
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    console.log("Full URL:", window.location.href);
    console.log("Search:", window.location.search);
    console.log("UID:", uid);
    console.log("TOKEN:", token);
    if (!uid || !token) {
      setStatus('error');
      setErrorMessage('This verification link is missing required information.');
      return;
    }
    authService.verifyEmail({ uid, token })
      .then((response) => {
       const { access, refresh, user } = response.data;

        tokenStorage.setAccessToken(access);
        tokenStorage.setRefreshToken(refresh);

        setUser(user);

        setStatus("success");

        setTimeout(() => {
          navigate("/dashboard", { replace: true });
        }, 1000);
      })
      .catch((error) => {
        console.log(error.response?.data);

        setStatus("error");

        setErrorMessage(
          extractApiError(error).message
        );
      });
  }, [uid, token]);

  return (
    <>
      <Helmet><title>Verify Email | AFC - Ahmad Foods</title></Helmet>
      <AuthCard title="Email Verification">
        {status === 'verifying' && <PageLoader />}
        {status === 'success' && (
          <div className="flex flex-col items-center gap-3 text-center">
            <FiCheckCircle className="h-10 w-10 text-success" />
            <p className="text-sm text-ink-700">
              Your email has been verified successfully. Redirecting to your dashboard...
            </p>

          </div>
        )}
        {status === 'error' && (
          <div className="flex flex-col items-center gap-3 text-center">
            <FiXCircle className="h-10 w-10 text-danger" />
            <p className="text-sm text-ink-700">{errorMessage}</p>
            <Link to="/login" className="text-sm font-semibold text-marigold-600 hover:underline">Back to login</Link>
          </div>
        )}
      </AuthCard>
    </>
  );
}
