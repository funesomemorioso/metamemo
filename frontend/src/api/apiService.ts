class ApiService {
  private baseUrl = import.meta.env.VITE_API_URL;

  async get<T>(path: string, params?: { [key: string]: any }): Promise<T> {
    const initialParams = [];

    // Convert object to arrays to be used by URLSearchParams
    if (params) {
      for (const param of Object.entries(params)) {
        if (!Array.isArray(param[1])) {
          initialParams.push([param[0],param[1]])
          continue
        }
        for (let i=0; i < param[1].length; i++) {
            initialParams.push([param[0],param[1][i]])
        }
      }
    }

    let resultParams = ""
    if (initialParams.length > 0) {
      const queryParams = new URLSearchParams(initialParams)
      resultParams = "?" + queryParams
    }

    const formatSymbol = (initialParams.length > 0) || path.includes("?") ? "&" : "?"
    const url = `${this.baseUrl}${path}${resultParams}${formatSymbol}format=json`;
    const response = await fetch(url.replace('%2B', '+'));
    const data = await response.json() as T;
    return data;
  }

}

export default new ApiService();
