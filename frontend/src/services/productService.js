import { createResourceService } from './createResourceService';

const base = createResourceService('/products/');

export const productService = {
  ...base,
  trending: (params) => base.listAction('trending', params),
  featured: (params) => base.listAction('featured', params),
  bestSellers: (params) => base.listAction('best-sellers', params),
};

export const addonService = createResourceService('/products/addons/');
