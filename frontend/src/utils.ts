// Utils functions

export const formatDate = (timestamp: number): string => {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  return `${year}-${month}-${day}`;
};

export const convertDateToUtc = (dateString: string): number => {
  const [year, month, day] = dateString.split("-").map(Number);
  const utcDate = Date.UTC(year, month - 1, day + 1);
  return utcDate;
};

export const parseDateString = (dateString: string): Date => {
  const [datePart, timePart] = dateString.split(" às ");
  const [day, month, year] = datePart.split("/").map(Number);
  const [hours, minutes, seconds] = timePart.split(":").map(Number);
  const date = new Date(year, month - 1, day, hours, minutes, seconds);
  return date;
};

export const formatDateHour = (
  dateHourUTC: string,
  locale: string = "pt-BR",
  separatorString: string = "às"
) => {
  const dateHour = new Date(dateHourUTC);
  const dateFormated = dateHour.toLocaleDateString(locale);
  const hourFormated = dateHour.toLocaleTimeString(locale);
  return `${dateFormated} ${separatorString} ${hourFormated}`;
};

export const formatToApi = (
  form: {
    selectedPeople: [];
    socialMedia: [];
    searchText: string;
    dateRange: number[];
  },
  page: number,
  pageSize: number,
  sorter: { order: string; columnKey: string }
) => {
  const routerResult: {
    page_size?: number;
    page?: number;
    sort_by?: string;
    sort_order?: string;
    author?: any[];
    source?: any[];
    content?: string;
    start_date?: string;
    end_date?: string;
  } = {};

  let author: string | any[] = [...form.selectedPeople];
  if (author.length > 0) {
    routerResult.author = author;
  }

  let source: string | any[] = [...form.socialMedia];
  if (source.length > 0) {
    routerResult.source = source;
  }

  let content = form.searchText;
  if (content) {
    routerResult.content = content;
  }

  let startDate = "";
  let endDate = "";

  if (form.dateRange) {
    startDate = formatDate(form.dateRange[0]);
    endDate = formatDate(form.dateRange[1]);

    routerResult.start_date = startDate;
    routerResult.end_date = endDate;
  }

  if (pageSize > 10) {
    routerResult.page_size = pageSize;
  }
  if (page > 1) {
    routerResult.page = page;
  }
  if (sorter?.order) {
    routerResult.sort_by = sorter.columnKey;
    routerResult.sort_order = sorter.order;
  }

  return routerResult;
};

export const urlUpdateWithState = async (
  store: {
    state: {
      form: {
        selectedPeople: [];
        socialMedia: [];
        searchText: string;
        dateRange: number[];
      },
      page: number,
      pageSize: number,
      sorter: { order: string; columnKey: string },
      tab: string
    }}
) => {
  const form = store.state.form;
  const page = store.state.page;
  const pageSize = store.state.pageSize;
  const sorter = store.state.sorter;
  const routerResult = formatToApi(form, page, pageSize, sorter);
  const tab = store.state.tab;

  return { path: `/consulta/${tab}/`, query: routerResult };
};
