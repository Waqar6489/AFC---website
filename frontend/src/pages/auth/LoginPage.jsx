import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Helmet } from 'react-helmet-async';
import AuthCard from '@/components/common/AuthCard';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import { extractApiError } from '@/services/apiClient';
import { authService } from '@/services/authService';

export default function LoginPage() {
  const [showResend, setShowResend] = useState(false);
  const [emailForResend, setEmailForResend] = useState('');
  const [isResending, setIsResending] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const redirectTo = location.state?.from?.pathname || '/dashboard';

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm();

  async function onSubmit(values) {
    try {
      setEmailForResend(values.email);
      setShowResend(false);

      await login(values);

      toast.success('Welcome back!');
      navigate(redirectTo, { replace: true });
    } catch (error) {
      const { message, fieldErrors } = extractApiError(error);

      Object.entries(fieldErrors).forEach(([field, messages]) => {
        setError(field === 'non_field_errors' ? 'root' : field, {
          message: messages[0],
        });
      });

      if (!Object.keys(fieldErrors).length) {
        setError('root', { message });
      }

      if (message.toLowerCase().includes('verify')) {
        setShowResend(true);
      }

      toast.error(message);
    }
  }

  async function handleResendVerification() {
    try {
      setIsResending(true);

      await authService.resendVerification(emailForResend);

      toast.success('Verification email sent successfully.');
    } catch (error) {
      toast.error(extractApiError(error).message);
    } finally {
      setIsResending(false);
    }
  }

  return (
    <>
      <Helmet><title>Login | AFC - Ahmad Foods</title></Helmet>
      <AuthCard
        title="Welcome back"
        subtitle="Log in to your AFC account"
        footer={<>Don&apos;t have an account? <Link to="/register" className="font-semibold text-marigold-600">Register</Link></>}
      >
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
          <Input
            label="Email"
            type="email"
            autoComplete="email"
            error={errors.email?.message}
            {...register('email', { required: 'Email is required' })}
          />
          <Input
            label="Password"
            type="password"
            autoComplete="current-password"
            error={errors.password?.message}
            {...register('password', { required: 'Password is required' })}
          />
          <div className="-mt-1 text-right">
            <Link to="/forgot-password" className="text-xs font-medium text-marigold-600 hover:underline">
              Forgot password?
            </Link>
          </div>
          {errors.root && <p className="text-sm text-danger">{errors.root.message}</p>}
          {showResend && (
            <button
              type="button"
              onClick={handleResendVerification}
              disabled={isResending}
              className="text-sm font-medium text-marigold-600 hover:underline disabled:opacity-50"
            >
              {isResending
                ? 'Sending...'
                : 'Resend Verification Email'}
            </button>
          )}
          <Button type="submit" isLoading={isSubmitting} className="mt-1 w-full">
            Log In
          </Button>
        </form>
      </AuthCard>
    </>
  );
}
