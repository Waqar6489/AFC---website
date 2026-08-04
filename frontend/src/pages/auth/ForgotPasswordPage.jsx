import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import AuthCard from '@/components/common/AuthCard';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { authService } from '@/services/authService';
import { extractApiError } from '@/services/apiClient';

export default function ForgotPasswordPage() {
  const [isSent, setIsSent] = useState(false);
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm();

  async function onSubmit({ email }) {
    try {
      await authService.forgotPassword(email);
      setIsSent(true);
    } catch (error) {
      // The backend intentionally returns the same success response
      // whether or not the email exists (prevents enumeration), so a
      // request-level error here means something else went wrong.
      setIsSent(false);
      throw new Error(extractApiError(error).message);
    }
  }

  return (
    <>
      <Helmet><title>Forgot Password | AFC - Ahmad Foods</title></Helmet>
      <AuthCard
        title="Reset your password"
        subtitle="We'll email you a link to reset it"
        footer={<Link to="/login" className="font-semibold text-marigold-600">Back to login</Link>}
      >
        {isSent ? (
          <p className="text-sm text-ink-600">
            If an account exists with that email, a password reset link is on its way. Please check your inbox.
          </p>
        ) : (
          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
            <Input
              label="Email"
              type="email"
              autoComplete="email"
              error={errors.email?.message}
              {...register('email', { required: 'Email is required' })}
            />
            <Button type="submit" isLoading={isSubmitting} className="w-full">
              Send Reset Link
            </Button>
          </form>
        )}
      </AuthCard>
    </>
  );
}
