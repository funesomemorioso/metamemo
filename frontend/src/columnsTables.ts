import Blogger from "@vicons/fa/Blogger";
import Link from "@vicons/carbon/Link";
import LogoFacebook from "@vicons/carbon/LogoFacebook";
import LogoInstagram from "@vicons/carbon/LogoInstagram";
import LogoTwitter from "@vicons/carbon/LogoTwitter";
import LogoYoutube from "@vicons/carbon/LogoYoutube";
import TelegramTwotone from "@vicons/material/TelegramTwotone";

import { NBadge, NText, NButton, NIcon, NImage, NEllipsis } from "naive-ui";
import { linkify, formatDateHour } from "./utils";
import type { SortOrder } from "naive-ui/es/data-table/src/interface";
import { h } from "vue";

import type { DataTableColumns } from "naive-ui";
import type { Ref } from "vue";

type RowData = {
  title: string;
  url: string;
  source: string;
  midia: string;
  media_urls: [];
  media_url: [];
  start_date?: string;
  end_date?: string;
  context?: string;
  media?: string;
  transcription?: string;
  original_url?: string;
};

const setIcon = (source: string) => {
  // Define icon and icon color
  let sourceIcon = {
    icon: Link,
    color: "text-gray-600 dark:text-gray-200",
  };

  if (source == "Twitter") {
    sourceIcon = {
      icon: LogoTwitter,
      color: "text-sky-600 dark:text-sky-500",
    };
  } else if (source == "Telegram") {
    sourceIcon = {
      icon: TelegramTwotone,
      color: "text-gray-500 dark:text-gray-400",
    };
  } else if (source == "Youtube") {
    sourceIcon = {
      icon: LogoYoutube,
      color: "text-rose-600 dark:text-rose-500",
    };
  } else if (source == "Facebook") {
    sourceIcon = {
      icon: LogoFacebook,
      color: "text-blue-600 dark:text-blue-500",
    };
  } else if (source == "Instagram") {
    sourceIcon = {
      icon: LogoInstagram,
      color: "text-pink-600 dark:text-pink-500",
    };
  } else if (source == "Blog") {
    sourceIcon = {
      icon: Blogger,
      color: "text-orange-600 dark:text-orange-500",
    };
  }

  return sourceIcon;
};

const emptyResult = h(
  NText,
  { depth: 3, italic: true },
  { default: () => "(vazio)" }
);

export const createColumns = (
  tab: string,
  sorter: {
    columnKey: string;
    order: SortOrder;
  },
  showModalRef: Ref,
  modalContent: Ref
): DataTableColumns<RowData> => {
  let result: DataTableColumns<RowData> = [];

  if (tab === "lista") {
    result = [
      {
        title: "Conteúdo",
        key: "title",
        width: 400,
        sorter: true,
        sortOrder: sorter?.columnKey === "title" ? sorter.order : undefined,
        render(row) {
          const title = row.title;
          if (!title) {
            return emptyResult;
          }
          return h("div", {
            class:
              "p-2 rounded transition ease-in-out hover:bg-sky-100 dark:hover:bg-gray-700 hover:shadow",
            innerHTML: `${linkify(String(title))}`,
          });
        },
      },
      {
        title: "Rede",
        key: "source",
        width: 100,
        render(row) {
          let url = row.url;
          const source = row.source;
          const sourceIcon = setIcon(source);

          if (source == "Telegram") {
            url = row.midia;
          }

          if (!url) {
            return emptyResult;
          }

          return h(
            NButton,
            {
              strong: true,
              secondary: true,
              style: "padding: 8px",
              title: url,
              onClick: () => {
                window.open(String(url), "_blank");
              },
            },
            () =>
              h(NIcon, {
                size: "1.12rem",
                class: sourceIcon.color,
                component: h(sourceIcon.icon),
              })
          );
        },
      },
      {
        title: "Data e Hora",
        key: "content_date",
        width: 220,
        sorter: true,
        sortOrder:
          sorter?.columnKey === "content_date" ? sorter.order : undefined,
      },
      {
        title: "Autor",
        key: "author",
        width: 220,
        sorter: true,
        sortOrder: sorter?.columnKey === "author" ? sorter.order : undefined,
      },
      {
        title: "Midia",
        key: "midia",
        width: 220,
        render(row) {
          const mediaUrls = row.media_urls;
          if (!mediaUrls || mediaUrls.length === 0) {
            return emptyResult;
          }
          return h(
            NBadge,
            {
              value: mediaUrls.length,
              show: mediaUrls.length > 1,
            },
            () =>
              h(
                NButton,
                {
                  strong: true,
                  secondary: true,
                  style: "padding: 8px; margin-right: 8px",
                  title: "Clique para visualizar conteúdos",
                  onClick: () => {
                    showModalRef.value = true;
                    modalContent.value = row;
                  },
                },
                () =>
                  h(NIcon, {
                    size: "1.12rem",
                    component: h(Link),
                  })
              )
          );
        },
      },
    ];
  } else if (tab === "news") {
    result = [
      {
        title: "Manchete",
        key: "title",
        width: 400,
        sorter: true,
        sortOrder: sorter?.columnKey === "title" ? sorter.order : undefined,
        render(row) {
          const title = row.title;
          if (!title) {
            return emptyResult;
          }
          return h("div", {
            class:
              "p-2 rounded transition ease-in-out hover:bg-sky-100 dark:hover:bg-gray-700 hover:shadow",
            innerHTML: `${linkify(String(title))}`,
          });
        },
      },
      {
        title: "Veículo",
        key: "source",
        width: 170,
        sorter: true,
        sortOrder: sorter?.columnKey === "source" ? sorter.order : undefined,
        render(row) {
          const text = row.source;
          if (!text) {
            return emptyResult;
          }
          return h("div", {
            class: "italic",
            innerHTML: String(text),
          });
        },
      },
      {
        title: "Data e Hora",
        key: "content_date",
        width: 220,
        sorter: true,
        sortOrder:
          sorter?.columnKey === "content_date" ? sorter.order : undefined,
      },
      {
        title: "Link",
        key: "source",
        width: 100,
        render(row) {
          let url = row.url;
          if (!url) {
            return emptyResult;
          }

          const source = row.source;
          const sourceIcon = setIcon(source);

          return h(
            NButton,
            {
              strong: true,
              secondary: true,
              style: "padding: 8px",
              title: url,
              onClick: () => {
                window.open(String(url), "_blank");
              },
            },
            () =>
              h(NIcon, {
                size: "1.12rem",
                class: sourceIcon.color,
                component: h(sourceIcon.icon),
              })
          );
        },
      },
    ];
  } else if (tab === "contexts") {
    result = [
      {
        title: "Contexto",
        key: "context",
        width: 400,
        sorter: true,
        sortOrder: sorter?.columnKey === "title" ? sorter.order : undefined,
        render(row) {
          const title = row.context;
          if (!title) {
            return emptyResult;
          }
          return h("div", {
            class:
              "p-2 rounded transition ease-in-out hover:bg-sky-100 dark:hover:bg-gray-700 hover:shadow",
            innerHTML: `${linkify(String(title))}`,
          });
        },
      },
      {
        title: "Período",
        key: "start_date",
        width: 220,
        sorter: true,
        sortOrder:
          sorter?.columnKey === "start_date" ? sorter.order : undefined,
        render(row) {
          const startDate = formatDateHour(String(row.start_date), true);
          const endDate = formatDateHour(String(row.end_date), true);
          return h("div", {
            innerHTML:
              startDate !== endDate ? `${startDate} - ${endDate}` : startDate,
          });
        },
      },
      {
        title: "Link",
        key: "source",
        width: 100,
        render(row) {
          let url = row.url;
          if (!url) {
            return emptyResult;
          }

          const source = row.source;
          const sourceIcon = setIcon(source);

          return h(
            NButton,
            {
              strong: true,
              secondary: true,
              style: "padding: 8px",
              title: url,
              onClick: () => {
                window.open(String(url), "_blank");
              },
            },
            () =>
              h(NIcon, {
                size: "1.12rem",
                class: sourceIcon.color,
                component: h(sourceIcon.icon),
              })
          );
        },
      },
    ];
  } else if (tab === "newscovers") {
    result = [
      {
        title: "Capa",
        key: "context",
        width: 150,
        render(row) {
          const cover = row.media;
          if (!cover) {
            return emptyResult;
          }
          return h(NImage, {
            src: cover,
            width: "170",
            fallbackSrc: "https://placehold.co/600x400"
          });
        },
      },
      {
        title: "Veículo",
        key: "source",
        width: 170,
        sorter: true,
        sortOrder: sorter?.columnKey === "source" ? sorter.order : undefined,
        render(row) {
          const text = row.source;
          if (!text) {
            return emptyResult;
          }
          return h("div", {
            class: "italic",
            innerHTML: String(text),
          });
        },
      },
      {
        title: "Data e hora",
        key: "content_date",
        width: 220,
        sorter: true,
        sortOrder:
          sorter?.columnKey === "content_date" ? sorter.order : undefined,
      },
    ];
  } else if (tab === "transcricao") {
    result = [
      {
        title: "Transcrição",
        key: "transcription",
        width: 320,
        sorter: true,
        sortOrder:
          sorter?.columnKey === "transcription" ? sorter.order : undefined,
        render(row) {
          const text = row.transcription;
          if (!text) {
            return emptyResult;
          }
          return  h(NEllipsis, {
            expandTrigger:"click",
            lineClamp:"6",
            tooltip: false,
            class:
              "px-2 py-1 rounded transition ease-in-out hover:bg-sky-100 dark:hover:bg-gray-700 hover:shadow",
          },
          () => String(text)
          )}
      },
      {
        title: "Rede",
        key: "source",
        width: 100,
        render(row) {
          let url = row.original_url;
          const source = row.source;
          const sourceIcon = setIcon(source);

          if (!url) {
            return emptyResult;
          }

          return h(
            NButton,
            {
              strong: true,
              secondary: true,
              style: "padding: 8px",
              title: url,
              onClick: () => {
                window.open(String(url), "_blank");
              },
            },
            () =>
              h(NIcon, {
                size: "1.12rem",
                class: sourceIcon.color,
                component: h(sourceIcon.icon),
              })
          );
        },
      },
      {
        title: "Midia",
        key: "midia",
        width: 220,
        render(row) {
          const mediaUrl = row.media_url;
          if (!mediaUrl) {
            return emptyResult;
          }
          return h(
            NButton,
            {
              strong: true,
              secondary: true,
              style: "padding: 8px; margin-right: 8px",
              title: "Clique para visualizar conteúdos",
              onClick: () => {
                showModalRef.value = true;
                modalContent.value.media_urls = [row];
              },
            },
            () =>
            h(NIcon, {
              size: "1.12rem",
              component: h(Link),
            })
          )
        },
      },
    ];
  }

  return result;
};
