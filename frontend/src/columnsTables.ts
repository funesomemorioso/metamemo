import Blogger from "@vicons/fa/Blogger";
import Link from "@vicons/carbon/Link";
import LogoFacebook from "@vicons/carbon/LogoFacebook";
import LogoInstagram from "@vicons/carbon/LogoInstagram";
import LogoTwitter from "@vicons/carbon/LogoTwitter";
import LogoYoutube from "@vicons/carbon/LogoYoutube";
import TelegramTwotone from "@vicons/material/TelegramTwotone";

import { NBadge, NText, NButton, NIcon } from "naive-ui";
import { linkify } from "./utils";
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
};

const emptyResult = h(
  NText,
  { depth: 3, italic: true },
  { default: () => "(vazio)" }
);

export const createColumns = (
  sorter: {
    columnKey: string;
    order: SortOrder;
  },
  showModalRef: Ref,
  modalContent: Ref
): DataTableColumns<RowData> => {
  return [
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
          url = row.midia;
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
                title: "Clique para visualizar elmentos",
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
};
