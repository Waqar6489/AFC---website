import { useForm } from 'react-hook-form';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Helmet } from 'react-helmet-async';
import AuthCard from '@/components/common/AuthCard';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { authService } from '@/services/authService';
import { extractApiError } from '@/services/apiClient';

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const uid = searchParams.get('uid');
  const token = searchParams.get('token');
  const navigate = useNavigate();

  const { register, handleSubmit, watch, setError, formState: { errors, isSubmitting } } = useForm();

  const linkIsMissing = !uid || !token;

  async function onSubmit(values) {
    try {
      await authService.resetPassword({ uid, token, ...values });
      toast.success('Password reset! You can now log in.');
      navigate('/login');
    } catch (error) {
      const { message, fieldErrors } = extractApiError(error);
      Object.entries(fieldErrors).forEach(([field, messages]) => {
        setError(field === 'non_field_errors' ? 'root' : field, { message: messages[0] });
      });
      if (!Object.keys(fieldErrors).length) setError('root', { message });
      toast.error(message);
    }
  }

  return (
    <>
      <Helmet><title>Reset Password | AFC - Ahmad Foods</title></Helmet>
      <AuthCard
        title="Choose a new password"
        footer={<Link to="/login" className="font-semibold text-marigold-600">Back to login</Link>}
      >
        {linkIsMissing ? (
          <p className="text-sm text-danger">
            This reset link is invalid or incomplete. Please request a new one from the{' '}
            <Link to="/forgot-password" className="font-semibold underline">forgot password</Link> page.
          </p>
        ) : (
          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
            <Input
              label="New password"
              type="password"
              autoComplete="new-password"
              error={errors.new_password?.message}
              {...register('new_password', { required: 'Password is required', minLength: { value: 8, message: 'At least 8 characters' } })}
            />
            <Input
              label="Confirm new password"
              type="password"
              autoComplete="new-password"
              error={errors.new_password_confirm?.message}
              {...register('new_password_confirm', {
                required: 'Please confirm your password',
                validate: (value) => value === watch('new_password') || 'Passwords do not match',
              })}
            />
            {errors.root && <p className="text-sm text-danger">{errors.root.message}</p>}
            <Button type="submit" isLoading={isSubmitting} className="w-full">
              Reset Password
            </Button>
          </form>
        )}
      </AuthCard>
    </>
  );
}
