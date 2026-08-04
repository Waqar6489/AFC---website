import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Helmet } from 'react-helmet-async';
import toast from 'react-hot-toast';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import { useAuth } from '@/hooks/useAuth';
import { accountService } from '@/services/accountService';
import { extractApiError } from '@/services/apiClient';

export default function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const { register, handleSubmit, reset, formState: { errors, isSubmitting, isDirty } } = useForm();

  useEffect(() => {
    if (user) reset({ first_name: user.first_name, last_name: user.last_name, phone: user.phone });
  }, [user, reset]);

  async function onSubmit(values) {
    try {
      await accountService.updateProfile(values);
      await refreshUser();
      toast.success('Profile updated.');
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  return (
    <>
      <Helmet><title>Profile | AFC - Ahmad Foods</title></Helmet>
      <h1 className="text-2xl font-bold text-ink-900">Profile</h1>

      <div className="mt-6 max-w-lg rounded-[var(--radius-card)] border border-ink-100 bg-white p-6">
        <div className="mb-5 flex items-center justify-between">
          <div>
            <p className="text-sm text-ink-400">Email</p>
            <p className="font-medium text-ink-800">{user?.email}</p>
          </div>
          <Badge variant={user?.is_email_verified ? 'success' : 'outline'}>
            {user?.is_email_verified ? 'Verified' : 'Unverified'}
          </Badge>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
          <div className="grid grid-cols-2 gap-3">
            <Input label="First name" error={errors.first_name?.message} {...register('first_name', { required: 'Required' })} />
            <Input label="Last name" error={errors.last_name?.message} {...register('last_name')} />
          </div>
          <Input label="Phone" type="tel" placeholder="+923001234567" error={errors.phone?.message} {...register('phone')} />
          <Button type="submit" isLoading={isSubmitting} disabled={!isDirty} className="w-fit">
            Save Changes
          </Button>
        </form>
      </div>
    </>
  );
}
