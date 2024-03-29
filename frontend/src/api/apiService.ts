class ApiService {
  private baseUrl = import.meta.env.VITE_API_URL;

  formatQuery({ params, format }: { params?: { [key: string]: any }, format?: string }) {
    const initialParams = [["format", format ? format : "json"]];
    // Convert object to arrays to be used by URLSearchParams
    if (params) {
      for (const param of Object.entries(params)) {
        if (!Array.isArray(param[1])) {
          initialParams.push([param[0], param[1]])
          continue
        }
        for (let i = 0; i < param[1].length; i++) {
          initialParams.push([param[0], param[1][i]])
        }
      }
    }

    let resultParams = '?' + (new URLSearchParams(initialParams))
    return resultParams
  }

  async get<T>(path: string, params?: { [key: string]: any }, format = "json"): Promise<T> {
    const resultParams = this.formatQuery({ params, format });
    const url = `${this.baseUrl}${path}${resultParams}`;
    const response = await fetch(url.replace("%2B", "+"));
    const data = (await response.json()) as T;
    return data;
  }
}

export default new ApiService();
