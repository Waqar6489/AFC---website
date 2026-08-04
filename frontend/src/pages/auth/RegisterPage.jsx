import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Helmet } from 'react-helmet-async';
import AuthCard from '@/components/common/AuthCard';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import { extractApiError } from '@/services/apiClient';

export default function RegisterPage() {
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    setError,
    formState: { errors, isSubmitting },
  } = useForm();

  async function onSubmit(values) {
    try {
      await registerUser(values);

      toast.success('Account created! Please verify your email.');

     navigate('/check-email', {
  state: {
    email: values.email,
  },
});
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
      <Helmet><title>Create Account | AFC - Ahmad Foods</title></Helmet>
      <AuthCard
        title="Create your account"
        subtitle="Join AFC to start ordering"
        footer={<>Already have an account? <Link to="/login" className="font-semibold text-marigold-600">Log in</Link></>}
      >
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
          <div className="grid grid-cols-2 gap-3">
            <Input
              label="First name"
              autoComplete="given-name"
              error={errors.first_name?.message}
              {...register('first_name', { required: 'Required' })}
            />
            <Input
              label="Last name"
              autoComplete="family-name"
              error={errors.last_name?.message}
              {...register('last_name')}
            />
          </div>
          <Input
            label="Email"
            type="email"
            autoComplete="email"
            error={errors.email?.message}
            {...register('email', { required: 'Email is required' })}
          />
          <Input
            label="Phone (optional)"
            type="tel"
            autoComplete="tel"
            placeholder="+923001234567"
            error={errors.phone?.message}
            {...register('phone')}
          />
          <Input
            label="Password"
            type="password"
            autoComplete="new-password"
            error={errors.password?.message}
            {...register('password', { required: 'Password is required', minLength: { value: 8, message: 'At least 8 characters' } })}
          />
          <Input
            label="Confirm password"
            type="password"
            autoComplete="new-password"
            error={errors.password_confirm?.message}
            {...register('password_confirm', {
              required: 'Please confirm your password',
              validate: (value) => value === watch('password') || 'Passwords do not match',
            })}
          />
          {errors.root && <p className="text-sm text-danger">{errors.root.message}</p>}
          <Button type="submit" isLoading={isSubmitting} className="mt-1 w-full">
            Create Account
          </Button>
        </form>
      </AuthCard>
    </>
  );
}
