import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { Helmet } from 'react-helmet-async';
import toast from 'react-hot-toast';
import { FiMapPin, FiPlus, FiTrash2 } from 'react-icons/fi';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import EmptyState from '@/components/ui/EmptyState';
import PageLoader from '@/components/ui/PageLoader';
import { accountService } from '@/services/accountService';
import { extractApiError } from '@/services/apiClient';

export default function AddressesPage() {
  const [addresses, setAddresses] = useState(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm();

  function loadAddresses() {
    accountService.addresses.list().then((data) => setAddresses(data.results ?? data));
  }

  useEffect(loadAddresses, []);

  async function onSubmit(values) {
    try {
      await accountService.addresses.create({ ...values, label: 'home' });
      toast.success('Address saved.');
      reset();
      setIsFormOpen(false);
      loadAddresses();
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  async function handleDelete(id) {
    try {
      await accountService.addresses.remove(id);
      loadAddresses();
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  if (addresses === null) return <PageLoader />;

  return (
    <>
      <Helmet><title>Addresses | AFC - Ahmad Foods</title></Helmet>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-ink-900">Addresses</h1>
        <Button size="sm" onClick={() => setIsFormOpen((open) => !open)}>
          <FiPlus className="h-4 w-4" /> Add Address
        </Button>
      </div>

      {isFormOpen && (
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="mt-5 grid grid-cols-1 gap-3 rounded-[var(--radius-card)] border border-ink-100 bg-white p-5 sm:grid-cols-2"
          noValidate
        >
          <Input label="Full name" error={errors.full_name?.message} {...register('full_name', { required: 'Required' })} />
          <Input label="Phone" type="tel" placeholder="+923001234567" error={errors.phone?.message} {...register('phone', { required: 'Required' })} />
          <Input label="Address line" className="sm:col-span-2" error={errors.address_line?.message} {...register('address_line', { required: 'Required' })} />
          <Input label="City" error={errors.city?.message} {...register('city', { required: 'Required' })} />
          <div />
          <Input
            label="Latitude"
            type="number"
            step="any"
            error={errors.latitude?.message}
            {...register('latitude', { required: 'Required', valueAsNumber: true })}
          />
          <Input
            label="Longitude"
            type="number"
            step="any"
            error={errors.longitude?.message}
            {...register('longitude', { required: 'Required', valueAsNumber: true })}
          />
          <p className="text-xs text-ink-400 sm:col-span-2">
            Latitude/longitude will be captured automatically from your browser at checkout — this manual entry is a fallback for the dashboard.
          </p>
          <Button type="submit" isLoading={isSubmitting} className="w-fit sm:col-span-2">Save Address</Button>
        </form>
      )}

      {addresses.length === 0 ? (
        <EmptyState icon={FiMapPin} title="No saved addresses" description="Add a delivery address to speed up checkout." className="mt-6" />
      ) : (
        <ul className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
          {addresses.map((address) => (
            <li key={address.id} className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold text-ink-800">{address.full_name}</p>
                  <p className="text-sm text-ink-500">{address.address_line}, {address.city}</p>
                  <p className="text-sm text-ink-400">{address.phone}</p>
                </div>
                <button onClick={() => handleDelete(address.id)} aria-label="Delete address" className="text-ink-300 hover:text-danger">
                  <FiTrash2 className="h-4 w-4" />
                </button>
              </div>
              {address.is_default && <Badge className="mt-2">Default</Badge>}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
