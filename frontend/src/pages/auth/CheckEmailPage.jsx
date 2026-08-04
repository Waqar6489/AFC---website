import { Link, useLocation } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { FiMail } from 'react-icons/fi';
import { useState } from 'react';
import toast from 'react-hot-toast';

import AuthCard from '@/components/common/AuthCard';
import Button from '@/components/ui/Button';
import { authService } from '@/services/authService';
import { extractApiError } from '@/services/apiClient';

export default function CheckEmailPage() {
  const location = useLocation();
  const email = location.state?.email || '';

  const [isResending, setIsResending] = useState(false);

  async function handleResendVerification() {
    if (!email) {
      toast.error('Email address not found.');
      return;
    }

    try {
      setIsResending(true);

      await authService.resendVerification(email);

      toast.success('Verification email sent successfully.');
    } catch (error) {
      toast.error(extractApiError(error).message);
    } finally {
      setIsResending(false);
    }
  }

  return (
    <>
      <Helmet>
        <title>Check Your Email | AFC - Ahmad Foods</title>
      </Helmet>

      <AuthCard title="Check Your Email">
        <div className="flex flex-col items-center gap-4 text-center">

          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-marigold-100">
            <FiMail className="h-8 w-8 text-marigold-600" />
          </div>

          <p>Your account has been created successfully.</p>

          <p className="text-sm text-ink-600">
            We've sent a verification email to
          </p>

          <p className="font-semibold text-marigold-600 break-all">
            {email}
          </p>

          <p className="text-sm text-ink-500">
            Please open your inbox and click the verification link to activate your account.
          </p>

          <Button
            type="button"
            onClick={handleResendVerification}
            isLoading={isResending}
            className="w-full"
          >
            Resend Verification Email
          </Button>

          <Link
            to="/login"
            className="text-sm font-semibold text-marigold-600 hover:underline"
          >
            Back to Login
          </Link>

        </div>
      </AuthCard>
    </>
  );
}