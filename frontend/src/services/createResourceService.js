import { apiClient } from './apiClient';

/**
 * Builds a standard CRUD service for a DRF ViewSet-backed endpoint, so
 * individual service files don't each hand-roll the same five methods.
 * `basePath` must include the trailing slash DRF expects, e.g. "/products/".
 */
export function createResourceService(basePath) {
  return {
    list: (params = {}) => apiClient.get(basePath, { params }).then((res) => res.data),

    retrieve: (idOrSlug, params = {}) =>
      apiClient.get(`${basePath}${idOrSlug}/`, { params }).then((res) => res.data),

    create: (payload, config = {}) => apiClient.post(basePath, payload, config).then((res) => res.data),

    update: (idOrSlug, payload, config = {}) =>
      apiClient.patch(`${basePath}${idOrSlug}/`, payload, config).then((res) => res.data),

    replace: (idOrSlug, payload, config = {}) =>
      apiClient.put(`${basePath}${idOrSlug}/`, payload, config).then((res) => res.data),

    remove: (idOrSlug) => apiClient.delete(`${basePath}${idOrSlug}/`).then((res) => res.data),

    /** For @action(detail=False) custom endpoints, e.g. "trending", "active". */
    listAction: (action, params = {}) =>
      apiClient.get(`${basePath}${action}/`, { params }).then((res) => res.data),

    /** For @action(detail=True) custom endpoints, e.g. "{id}/update-status". */
    detailAction: (idOrSlug, action, payload = {}, method = 'post') =>
      apiClient[method](`${basePath}${idOrSlug}/${action}/`, payload).then((res) => res.data),
  };
}
