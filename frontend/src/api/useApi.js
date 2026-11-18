// Runs an API call whenever its dependencies change and tracks loading/error state.
import { useEffect, useState } from 'react';

export function useApi(request, deps) {
  const [state, setState] = useState({ data: null, error: null, loading: true });

  useEffect(() => {
    const controller = new AbortController();
    setState((current) => ({ data: current.data, error: null, loading: true }));

    request({ signal: controller.signal })
      .then((data) => setState({ data, error: null, loading: false }))
      .catch((error) => {
        if (error.name === 'AbortError') return;
        setState({ data: null, error, loading: false });
      });

    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}
